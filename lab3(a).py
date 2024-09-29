import random
def generate_k_sat(n, m, k=3):
    clauses = []
    for _ in range(m):
        clause = []
        variables = random.sample(range(1, n + 1), k)
        for var in variables:
            literal = var if random.choice([True, False]) else -var
            clause.append(literal)
        clauses.append(clause)
    return clauses

def evaluate_solution(clauses, solution):
    satisfied_clauses = 0
    for clause in clauses:
        clause_satisfied = False
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0 and solution[var] == True:
                clause_satisfied = True
            elif literal < 0 and solution[var] == False:
                clause_satisfied = True
        if clause_satisfied:
            satisfied_clauses += 1
    return satisfied_clauses

def hill_climbing(clauses, n):
    current_solution = [random.choice([True, False]) for _ in range(n)]
    current_score = evaluate_solution(clauses, current_solution)

    while True:
        improved = False
        for i in range(n):
            neighbor_solution = current_solution[:]
            neighbor_solution[i] = not neighbor_solution[i]
            neighbor_score = evaluate_solution(clauses, neighbor_solution)
            if neighbor_score > current_score:
                current_solution = neighbor_solution
                current_score = neighbor_score
                improved = True
                break
        if not improved:
            break

    return current_solution, current_score

def beam_search(clauses, n, beam_width):
    current_candidates = [[random.choice([True, False]) for _ in range(n)]]
    
    while current_candidates:
        new_candidates = []
        for candidate in current_candidates:
            for i in range(n):
                neighbor = candidate[:]
                neighbor[i] = not neighbor[i]
                new_candidates.append(neighbor)

        new_candidates = sorted(new_candidates, key=lambda x: evaluate_solution(clauses, x), reverse=True)
        current_candidates = new_candidates[:beam_width]

        if any(evaluate_solution(clauses, c) == len(clauses) for c in current_candidates):
            break

    return current_candidates[0], evaluate_solution(clauses, current_candidates[0])

def variable_neighborhood_descent(clauses, n):
    current_solution = [random.choice([True, False]) for _ in range(n)]
    current_score = evaluate_solution(clauses, current_solution)

    neighborhoods = [N1, N2, N3]

    for N in neighborhoods:
        while True:
            improved = False
            neighbors = N(current_solution)
            for neighbor in neighbors:
                neighbor_score = evaluate_solution(clauses, neighbor)
                if neighbor_score > current_score:
                    current_solution = neighbor
                    current_score = neighbor_score
                    improved = True
                    break
            if not improved:
                break

    return current_solution, current_score

def N1(solution):
    neighbors = []
    for i in range(len(solution)):
        neighbor = solution[:]
        neighbor[i] = not neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def N2(solution):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution[:]
            neighbor[i] = not neighbor[i]
            neighbor[j] = not neighbor[j]
            neighbors.append(neighbor)
    return neighbors

def N3(solution):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            for k in range(j + 1, len(solution)):
                neighbor = solution[:]
                neighbor[i] = not neighbor[i]
                neighbor[j] = not neighbor[j]
                neighbor[k] = not neighbor[k]
                neighbors.append(neighbor)
    return neighbors

def compare_algorithms(m_values, n_values, beam_widths):
    for n in n_values:
        for m in m_values:
            clauses = generate_k_sat(n, m)

            print(f"\nSolving for n={n}, m={m} (Number of variables: {n}, Number of clauses: {m}):")

            hc_solution, hc_score = hill_climbing(clauses, n)
            print(f"Hill Climbing: Score={hc_score}, Solution={hc_solution}")

            for beam_width in beam_widths:
                bs_solution, bs_score = beam_search(clauses, n, beam_width)
                print(f"Beam Search (beam width {beam_width}): Score={bs_score}, Solution={bs_solution}")

            vnd_solution, vnd_score = variable_neighborhood_descent(clauses, n)
            print(f"Variable Neighborhood Descent: Score={vnd_score}, Solution={vnd_solution}")

m_values = [10, 20]
n_values = [5, 10]
beam_widths = [3, 4]

compare_algorithms(m_values, n_values, beam_widths)