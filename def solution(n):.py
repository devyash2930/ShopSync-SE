def solution(segments):
    # Find the maximum byte value (end of all ranges)
    max_byte = max(end for _, end in segments)

    # Initialize a difference array
    diff = [0] * (max_byte + 2)  # +2 to handle 1-based indexing and boundary

    # Mark the start and end of each range in the diff array
    for start, end in segments:
        diff[start] += 1
        diff[end + 1] -= 1

    # Sweep through the diff array to calculate cumulative unique bytes
    unique_bytes = 0
    current_unique = 0
    result = []
    segment_index = 0

    # Use a set to track when we reach the end of a segment
    segment_ends = {end: idx for idx, (_, end) in enumerate(segments)}

    for i in range(1, max_byte + 1):
        current_unique += diff[i]
        if current_unique > 0:
            unique_bytes += 1
        # Check if this index corresponds to the end of a segment
        if i in segment_ends:
            result.append(unique_bytes)

    return result

# Example Input
segments = [[1, 9], [1, 3], [8, 15], [6, 9], [2, 5]]

# Example Output
print(solution(segments))  # Expected: [9, 3, 15, 9, 5]
