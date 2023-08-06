def format_report_csv(report):
    """Format JSON validation report as CSV string

    :param report: JSON report output from validator
    :return: string representing csv formatted report
    """
    output = str()
    if report['validation_finished']:
        output = "Validation=success\n"
    for warning in report['warnings']:
        output += str("{},{},{}\n").format(warning['code'], warning['message'], warning['supplemental'])
    for error in report['errors']:
        output += str("{},{},{}\n").format(error['code'], error['message'], error['supplemental'])
    return output


def detect_graph_process_pooling(G):
    from isatools.model.v1 import Process
    for process in [n for n in G.nodes() if isinstance(n, Process)]:
        if len(G.in_edges(process)) > 1:
            print("Possible process pooling detected on: ", process.id)


def contains(small_list, big_list):
    if len(small_list) == 0:
        return False
    for i in iter(range(len(big_list) - len(small_list) + 1)):
        for j in iter(range(len(small_list))):
            if big_list[i + j] != small_list[j]:
                break
        else:
            return i, i + len(small_list)
    return False