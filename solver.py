import copy

def isSolved(grid, tubeHeight=None):
    if tubeHeight is None:
        tubeHeight = max(len(t) for t in grid)
    for tube in grid:
        if len(tube) == 0:
            continue
        elif len(tube) < tubeHeight:
            return False
        elif tube.count(tube[0]) != tubeHeight: 
            return False
    return True

def isMoveValid(tubeHeight, fromTube, candidateTube):
    if not fromTube or len(candidateTube) == tubeHeight:
        return False
    
    colour = fromTube[-1]

    count = 0
    for ball in reversed(fromTube):
        if ball == colour:
            count += 1
        else:
            break
    
    free_space = tubeHeight - len(candidateTube)
    if free_space == 0:
        return False
    
    if len(candidateTube) == 0:
        if count == len(fromTube):  
            return False
        return True
    
    return candidateTube[-1] == colour and free_space >= count

def moveBalls(tubeHeight, fromTube, toTube):
    if not isMoveValid(tubeHeight, fromTube, toTube):
        return 0

    colour = fromTube[-1]
    count = 0

    
    for ball in reversed(fromTube):
        if ball == colour:
            count += 1
        else:
            break

    free_space = tubeHeight - len(toTube)
    count = min(count, free_space)

    for _ in range(count):
        toTube.append(fromTube.pop())

    return count

def gridToCanonicalString(grid):
    tubeStrings = []
    for tube in grid:
        tubeStrings.append(','.join(tube))
    sortedTubeStrings = sorted(tubeStrings)
    return ';'.join(sortedTubeStrings)

def solveGrid(grid, tubeHeight=None, visitedPositions=None, answer=None):
    if tubeHeight is None:
        tubeHeight = max(len(t) for t in grid)
    if visitedPositions is None:
        visitedPositions = set()
    if answer is None:
        answer = []

    visitedPositions.add(gridToCanonicalString(grid))

    for i in range(len(grid)):
        for j in range(len(grid)):
            if i == j:
                continue
            
            grid2 = copy.deepcopy(grid)
            moved = moveBalls(tubeHeight, grid2[i], grid2[j])
            if moved == 0:
                continue

            if isSolved(grid2, tubeHeight):
                answer.append((i, j))
                return True

            canon = gridToCanonicalString(grid2)
            if canon not in visitedPositions:
                solved = solveGrid(grid2, tubeHeight, visitedPositions, answer)
                if solved:
                    answer.append((i, j))
                    return True
    return False

def compress_answer(answer):
    compressed = []

    for move in answer:
        if compressed and compressed[-1] == move[::-1]:
            compressed.pop()
        else:
            compressed.append(move)
    
    return compressed

def solve(puzzle):
    grid = [list(map(str, stack)) for stack in puzzle]

    if isSolved(grid):
        print("Grid is already solved")
        return []

    answer = []
    visitedPositions = set()
    solved = solveGrid(grid, visitedPositions=visitedPositions, answer=answer)

    answer = compress_answer(answer)

    return answer[::-1] if solved else None