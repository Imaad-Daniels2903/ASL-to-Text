import math

def get_distance(pixel_cords : list[tuple[int]]) -> dict :
    fingers = get_chunks(pixel_cords, 4, [])
    distances = {}
    for x in range(3, -1, -1) :
        distances[f"pp{x}"] = []
        if not x == 0:
            distances[f"kk{x}"] = []
            
        for y in range(len(fingers)) :
            if x > 0 :
                distances[f"kk{x}"].append(round(math.sqrt((fingers[y][x][0] - fingers[y][x - 1][0])**2 + (fingers[y][x][1] - fingers[y][x - 1][1])**2), 2))
                
            if y > 0 :
                distances[f"pp{x}"].append(round(math.sqrt((fingers[y][x][0] - fingers[y - 1][x][0])**2 + (fingers[y][x][1] - fingers[y - 1][x][1])**2), 2))
    
    return distances


def get_chunks(data : list, chunks : int, output : list = []) -> list :
    if len(data) // chunks == 1 :
        output.append(data)
        return output
    
    else :
        output.append(data[:chunks])
        return get_chunks(data[chunks:], chunks, output)


def main() :
    data = [1, 2, 3, 4, 5, 6, 7]
    print(get_chunks(data, 2))
    
    data2 = [7, 6, 5, 4, 3, 2, 1]
    print(get_chunks(data2, 2, ))
        
if __name__ == "__main__" :
    main()