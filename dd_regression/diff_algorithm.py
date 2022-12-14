# This code is from https://blog.robertelder.org/diff-algorithm/
# https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.4.6927


def diff(e, f, i=0, j=0):
    #  Documented at http://blog.robertelder.org/diff-algorithm/
    N, M, L, Z = len(e), len(f), len(e) + len(f), 2 * min(len(e), len(f)) + 2
    if N > 0 and M > 0:
        w, g, p = N - M, [0] * Z, [0] * Z
        for h in range(0, (L // 2 + (L % 2 != 0)) + 1):
            for r in range(0, 2):
                c, d, o, m = (g, p, 1, 1) if r == 0 else (p, g, 0, -1)
                for k in range(-(h - 2 * max(0, h - M)), h - 2 * max(0, h - N) + 1, 2):
                    a = c[(k + 1) % Z] if (k == -h or k != h and c[(k - 1) % Z] < c[(k + 1) % Z]) else c[(
                                                                                                                     k - 1) % Z] + 1
                    b = a - k
                    s, t = a, b
                    while a < N and b < M and e[(1 - o) * N + m * a + (o - 1)] == f[(1 - o) * M + m * b + (o - 1)]:
                        a, b = a + 1, b + 1
                    c[k % Z], z = a, -(k - w)
                    if L % 2 == o and z >= -(h - o) and z <= h - o and c[k % Z] + d[z % Z] >= N:
                        D, x, y, u, v = (2 * h - 1, s, t, a, b) if o == 1 else (2 * h, N - a, M - b, N - s, M - t)
                        if D > 1 or (x != u and y != v):
                            return diff(e[0:x], f[0:y], i, j) + diff(e[u:N], f[v:M], i + u, j + v)
                        elif M > N:
                            return diff([], f[N:M], i + N, j + N)
                        elif M < N:
                            return diff(e[M:N], [], i + M, j + M)
                        else:
                            return []
    elif N > 0:  # Modify the return statements below if you want a different edit script format
        return [{"operation": "delete", "position_old": i + n} for n in range(0, N)]
    else:
        return [{"operation": "insert", "position_old": i, "position_new": j + n} for n in range(0, M)]


# def print_edit_sequence(es, s1, s2):
#     for e in es:
#         if isinstance(e, tuple):
#             for f in e:
#                 if f["operation"] == "delete":
#                     print("Delete " + str(s1[f["position_old"]]) + " from s1 at position " + str(f["position_old"])
#                           + " in s1.")
#                 else:
#                     print("Insert " + str(s2[f["position_new"]]) + " from s2 before position " + str(f["position_old"])
#                           + " into s1.")
#         else:
#             if e["operation"] == "delete":
#                 print("Delete " + str(s1[e["position_old"]]) + " from s1 at position " + str(e["position_old"])
#                       + " in s1.")
#             else:
#                 print("Insert " + str(s2[e["position_new"]]) + " from s2 before position " + str(e["position_old"])
#                       + " into s1.")


def print_edit_sequence(es, s1, s2):
    # cant print if position is before the end
    # print("edit sequence")
    # print(s1)
    # print(s2)
    for e in es:
        # print(e)
        if isinstance(e, tuple):
            for f in e:
                if f["operation"] == "delete":
                    print("Delete " + str(s1[f["position_old"]]) + " from s1 at position " + str(f["position_old"])
                          + " in s1.")
                else:
                    if f["position_old"] != len(s1):
                        # print("Insert " + str(s2[f["position_new"]]) + " from s2 before position " + str(
                        #     s1[f["position_old"]]) + " into s1.")
                        print("Insert " + str(s2[f["position_new"]]) + " from s2 before position " + str(
                            f["position_old"]) + " into s1.")
                    else:
                        # print("Insert " + str(s2[f["position_new"]]) + " from s2 after position " + str(
                        #     s1[f["position_old"]-1])
                        #       + " into s1.")
                        print("Insert " + str(s2[f["position_new"]]) + " from s2 before position " + str(
                            f["position_old"]) + " into s1.")
        else:
            if e["operation"] == "delete":
                print("Delete " + str(s1[e["position_old"]]) + " from s1 at position " + str(e["position_old"])
                      + " in s1.")
            else:
                if e["position_old"] != len(s1):
                    print("Insert " + str(s2[e["position_new"]]) + " from s2 before position " + str(e["position_old"])
                          + " into s1.")
                    # print("Insert " + str(s2[e["position_new"]]) + " from s2 before position " + str(
                    #     s1[e["position_old"]])
                    #       + " into s1.")
                else:
                    # print("Insert " + str(s2[e["position_new"]]) + " from s2 after position " + str(
                    #     s1[e["position_old"] - 1])
                    #       + " into s1.")
                    print("Insert " + str(s2[e["position_new"]]) + " from s2 before position " + str(e["position_old"])
                          + " into s1.")
