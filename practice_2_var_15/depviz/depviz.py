#!/usr/bin/env python3

import argparse
import sys
import os
import tarfile
import urllib.request
from collections import deque, defaultdict


# Парсинг аргументов: этап 1
def parse_args():
    parser = argparse.ArgumentParser(description="Dependency graph visualizer for Alpine APK packages")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL-адрес репозитория или путь к тестовому файлу")
    parser.add_argument("--mode", required=True, choices=["remote", "test"], help="remote = APK репозиторий, test = локальный файл")
    parser.add_argument("--output", required=True, help="Имя файла для визуализации графа (PNG)")
    parser.add_argument("--depth", required=True, type=int, help="Максимальная глубина обхода зависимостей")
    args = parser.parse_args()

    if args.depth < 1:
        print("Ошибка: глубина должна быть >= 1", file=sys.stderr)
        sys.exit(1)
    return args


# Сбор данных: этап 2
def fetch_apkindex(url):
    tmp_file = "/tmp/APKINDEX.tar.gz"
    try:
        urllib.request.urlretrieve(url, tmp_file)
    except Exception:
        print("Ошибка загрузки APKINDEX.tar.gz", file=sys.stderr)
        sys.exit(1)

    try:
        with tarfile.open(tmp_file, "r:gz") as tar:
            member = tar.extractfile("APKINDEX")
            if member is None:
                raise Exception("APKINDEX not found inside archive")
            return member.read().decode("utf-8").splitlines()
    except Exception:
        print("Ошибка чтения APKINDEX", file=sys.stderr)
        sys.exit(1)


def parse_apk_dependencies(index_lines):
    deps = defaultdict(list)
    current_pkg = None
    for line in index_lines:
        if line.startswith("P:"):
            current_pkg = line[2:].strip()
        elif line.startswith("D:") and current_pkg:
            raw = line[2:].strip().split()
            cleaned = [d for d in raw if not d.startswith("so:") and not d.startswith("cmd:")]
            deps[current_pkg].extend(cleaned)
    return deps


# Тестовые данные и BFS: этап 3
def load_test_repository(path):
    if not os.path.exists(path):
        print("Ошибка: тестовый файл не найден", file=sys.stderr)
        sys.exit(1)
    deps = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                pkg, rest = line.split(":")
                pkg = pkg.strip()
                children = rest.strip().split()
                deps[pkg] = children
    return deps


def build_dependency_graph(root, deps_map, max_depth):
    graph = defaultdict(list)
    visited = set([root])
    queue = deque([(root, 0)])
    while queue:
        pkg, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for dep in deps_map.get(pkg, []):
            graph[pkg].append(dep)
            if dep not in visited:
                visited.add(dep)
                queue.append((dep, depth + 1))
    return graph


# Порядок загрузки: этап 4
def get_load_order(graph, start_package):
    visited = set()
    subgraph = defaultdict(list)
    queue = deque([start_package])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for dep in graph.get(node, []):
            subgraph[node].append(dep)
            queue.append(dep)
    # Топологическая сортировка Kahn
    in_degree = {u: 0 for u in visited}
    for u in subgraph:
        for v in subgraph[u]:
            in_degree[v] += 1
    topo_queue = deque([u for u in visited if in_degree[u] == 0])
    load_order = []
    while topo_queue:
        node = topo_queue.popleft()
        load_order.append(node)
        for neighbor in subgraph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                topo_queue.append(neighbor)
    if len(load_order) != len(visited):
        print("Внимание! Граф содержит циклы. Порядок загрузки может быть неполным.")
    return load_order


# Визуализация: этап 5
def visualize_graph(graph, output_file="graph.png"):
    graphs_dir = "graphs"
    if not os.path.exists(graphs_dir):
        os.makedirs(graphs_dir)

    dot_file = os.path.join(graphs_dir, output_file.replace(".png", ".dot"))
    png_base = os.path.join(graphs_dir, output_file.replace(".png", ""))

    dot_content = "digraph dependencies {\n"
    for pkg, deps in graph.items():
        for dep in deps:
            dot_content += f'    "{pkg}" -> "{dep}";\n'
    dot_content += "}"

    with open(dot_file, "w", encoding="utf-8") as f:
        f.write(dot_content)

    try:
        import graphviz
        g = graphviz.Source(dot_content)
        g.render(png_base, format="png", cleanup=True)
        print(f"Граф успешно сохранён в {png_base}.png")
    except ImportError:
        print("Установите graphviz: pip install graphviz")
        print(f"DOT файл сохранён: {dot_file}")


def main():
    args = parse_args()

    print("Параметры:")
    print(f"package={args.package}")
    print(f"repo={args.repo}")
    print(f"mode={args.mode}")
    print(f"output={args.output}")
    print(f"depth={args.depth}")

    if args.mode == "remote":
        index_lines = fetch_apkindex(args.repo)
        deps_map = parse_apk_dependencies(index_lines)
    else:
        deps_map = load_test_repository(args.repo)

    if args.package not in deps_map:
        print("Пакет не найден в репозитории", file=sys.stderr)
        sys.exit(1)

    print("\nПрямые зависимости:", deps_map[args.package])
    graph = build_dependency_graph(args.package, deps_map, args.depth)
    print("\nПолный граф (до глубины):")
    for k, v in graph.items():
        print(k, "->", v)

    print("\nПорядок загрузки зависимостей:")
    load_order = get_load_order(graph, args.package)
    print(load_order)

    visualize_graph(graph, args.output)


if __name__ == "__main__":
    main()
