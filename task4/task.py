import json


def get_membership_value(x, points):

    sorted_points = sorted(points, key=lambda p: p[0])


    if x <= sorted_points[0][0]:
        return float(sorted_points[0][1])
    if x >= sorted_points[-1][0]:
        return float(sorted_points[-1][1])


    for i in range(len(sorted_points) - 1):
        x0, y0 = sorted_points[i]
        x1, y1 = sorted_points[i + 1]
        if x0 <= x <= x1:
            if x0 == x1:
                return float(y0)
            return float(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
    return 0.0


def main(temp_json, heat_json, rules_json, current_temp):


    temp_data = json.loads(temp_json)
    heat_data = json.loads(heat_json)
    rules = json.loads(rules_json)

    temp_terms = list(temp_data.values())[0]
    heat_terms = list(heat_data.values())[0]


    temp_membership = {}
    for term in temp_terms:
        temp_membership[term['id']] = get_membership_value(current_temp, term['points'])


    aggregated_output = {}

    for input_term_id, output_term_id in rules:
        weight = temp_membership.get(input_term_id, 0.0)
        if output_term_id not in aggregated_output:
            aggregated_output[output_term_id] = weight
        else:
            aggregated_output[output_term_id] = max(aggregated_output[output_term_id], weight)


    all_heat_x = [p[0] for term in heat_terms for p in term['points']]
    min_x, max_x = min(all_heat_x), max(all_heat_x)

    step = 0.1
    numerator = 0.0
    denominator = 0.0

    curr_x = float(min_x)
    while curr_x <= max_x:
        max_mu_x = 0.0
        for term in heat_terms:
            mu_rule = aggregated_output.get(term['id'], 0.0)
            mu_x = get_membership_value(curr_x, term['points'])

            combined_mu = min(mu_rule, mu_x)
            max_mu_x = max(max_mu_x, combined_mu)

        numerator += curr_x * max_mu_x
        denominator += max_mu_x
        curr_x += step

    if denominator == 0:
        return 0.0

    return numerator / denominator
