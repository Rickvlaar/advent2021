from util import console, parse_file_as_list, time_function

day_file = parse_file_as_list('input/day_12.txt')
test_file = parse_file_as_list('input/day_12_test.txt')


class Cave:

    def __init__(self, name: str):
        self.name: str = name
        self.small: bool = name.islower()
        self.connected_to: set[Cave] = set()

    def add_connected_cave(self, cave: 'Cave'):
        self.connected_to.add(cave)

    def __repr__(self):
        return f'{self.name}'


def create_cave_map_from_file(file):
    routes = [line.split('-') for line in file]

    cave_dict = {cave_name: Cave(cave_name) for cave_name, _ in routes}
    cave_dict.update({cave_name: Cave(cave_name) for _, cave_name in routes})

    for cave_name, connection in routes:
        if connection != 'start':
            cave_dict[cave_name].add_connected_cave(cave_dict[connection])

        if cave_name != 'start':
            cave_dict[connection].add_connected_cave(cave_dict[cave_name])

    return cave_dict


@time_function(10)
def go_indian_a(cave_dict: dict):
    start_cave = cave_dict.get('start')
    return go_cavin(start_cave, 0, set())


@time_function(10)
def go_indian_b(cave_dict: dict):
    start_cave = cave_dict.get('start')
    return go_cavin(start_cave, 0, set(), True)


def go_indian_c(cave_dict):
    start_cave = cave_dict.get('start')

    console.print(start_cave.go_down(start_cave))


def go_cavin(cave: Cave, route_count: int, visited_nodes: set, go_twice: bool = False) -> int:
    if cave.name == 'end':
        route_count += 1
        return route_count

    if cave.small:
        visited_nodes.add(cave.name)

    for conn_cave in cave.connected_to:
        if conn_cave.name not in visited_nodes:
            route_count = go_cavin(conn_cave, route_count, visited_nodes.copy(), go_twice)
        elif go_twice and conn_cave.name in visited_nodes:
            route_count = go_cavin(conn_cave, route_count, visited_nodes.copy(), False)

    return route_count


if __name__ == '__main__':
    twelf_a = go_indian_a(create_cave_map_from_file(day_file))
    twelf_b = go_indian_b(create_cave_map_from_file(day_file))

    console.print(f'solution 12A: {twelf_a}')
    console.print(f'solution 12B: {twelf_b}')
