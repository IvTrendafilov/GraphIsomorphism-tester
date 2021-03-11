from graph_io import load_graph, write_dot

with open('projectgraphs/colorref_smallexample_4_16.grl') as f:
    L = load_graph(f, read_list=True)


def find_color_matches(graph_list):
    base_graph = graph_list[0]
    check_graphs = graph_list[1:]
    remainder_graphs = []
    next_color = 0
    color_list = []
    for v in base_graph.vertices:
        if v.colornum not in color_list:
            color_list.append(v.colornum)
        if v.colornum >= next_color:
            next_color = v.colornum + 1
    c = 0
    stop = False
    while not stop:
        c += 1
        neighbor_colors = []
        for i in range(len(color_list)):
            neighbor_colors.append([])
        update_list = []
        for i in range(len(color_list)):
            update_list.append([])
        for v in range(len(base_graph)):
            neighbor_color = []
            for n in base_graph.vertices[v].neighbours:
                neighbor_color.append(n.colornum)
            neighbor_color = sorted(neighbor_color)
            color_index = color_list.index(base_graph.vertices[v].colornum)
            if len(neighbor_colors[color_index]) >= 1:
                if neighbor_color not in neighbor_colors[color_index]:
                    neighbor_colors[color_index].append(neighbor_color)
                    update_list[color_index].append([v, next_color])
                    color_list.append(next_color)
                    next_color += 1
                else:
                    index = neighbor_colors[color_index].index(neighbor_color)
                    neighbor_colors[color_index].append(neighbor_color)
                    update_list[color_index].append([v, update_list[color_index][index][1]])
            else:
                neighbor_colors[color_index].append(neighbor_color)
                update_list[color_index].append([v, base_graph.vertices[v].colornum])
        delete_list = []
        for graph in check_graphs:
            change_list = []
            fail = False
            for g in graph.vertices:
                if not fail:
                    color_index = color_list.index(g.colornum)
                    neighbor_color = []
                    for n in g.neighbours:
                        neighbor_color.append(n.colornum)
                    neighbor_color = sorted(neighbor_color)
                    index2 = 0
                    if neighbor_color in neighbor_colors[color_index]:
                        index2 = neighbor_colors[color_index].index(neighbor_color)
                    else:
                        delete_list.append(graph)
                        fail = True
                    change_list.append(update_list[color_index][index2][1])
            if not fail:
                for m in range(len(graph.vertices)):
                    graph.vertices[m].colornum = change_list[m]
        for i in delete_list:
            check_graphs.remove(i)
            remainder_graphs.append([i, c])

        stop = True
        for l in update_list:
            for j in l:
                if j[1] != base_graph.vertices[j[0]].colornum:
                    base_graph.vertices[j[0]].colornum = j[1]
                    stop = False
    print(len(color_list))
    isomorphs = [base_graph] + check_graphs
    return isomorphs, remainder_graphs


def degree_colouring(graph_list):
    for g in graph_list:
        for v in g.vertices:
            v.colornum = v.degree


def isomorphisms_from_list(graph_list):
    isomorph_list = []
    match_groups = find_color_matches(graph_list)
    isomorph_list.append(match_groups[0])
    if match_groups[1] == []:
        return isomorph_list
    mismatch_group = []
    c = 0
    for i in match_groups[1]:
        if i[1] != c:
            if mismatch_group != []:
                isomorph_list.append(isomorphisms_from_list(mismatch_group)[0])
            mismatch_group = []
            c = i[1]
        mismatch_group.append(i[0])
    isomorph_list.append(isomorphisms_from_list(mismatch_group)[0])
    return isomorph_list


graphs = L[0]
degree_colouring(L[0])
isomorph_list = isomorphisms_from_list(graphs)
for i in range(len(isomorph_list)):
    for j in range(len(isomorph_list[i])):
        if isomorph_list[i][j] in graphs:
            isomorph_list[i][j] = graphs.index(isomorph_list[i][j])
print(isomorph_list)
with open('woo1.dot', 'w') as f:
    write_dot(graphs[0], f)
with open('woo2.dot', 'w') as f:
    write_dot(graphs[1], f)
