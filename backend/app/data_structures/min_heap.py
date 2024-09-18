class MinHeapNode:
    def __init__(self, total_distance, total_time, agent, last_order=None):
        self.total_distance = total_distance
        self.total_time = total_time
        self.agent = agent
        self.last_order = last_order  # Track the last order assigned to the agent

    def __lt__(self, other):
        # Comparison logic to maintain the heap order
        if self.total_distance == other.total_distance:
            return self.total_time < other.total_time
        return self.total_distance < other.total_distance


class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, node):
        """Inserts a new node into the heap."""
        self.heap.append(node)
        self._sift_up(len(self.heap) - 1)

    def extract_min(self):
        """Extracts and returns the node with the smallest total_distance (and total_time if equal)."""
        if not self.heap:
            return None
        self._swap(0, len(self.heap) - 1)
        min_node = self.heap.pop()
        self._sift_down(0)
        return min_node

    def _sift_up(self, idx):
        """Moves the node at index 'idx' up to its correct position in the heap."""
        parent = (idx - 1) // 2
        if parent >= 0 and self.heap[idx] < self.heap[parent]:
            self._swap(idx, parent)
            self._sift_up(parent)

    def _sift_down(self, idx):
        """Moves the node at index 'idx' down to its correct position in the heap."""
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != idx:
            self._swap(idx, smallest)
            self._sift_down(smallest)

    def _swap(self, i, j):
        """Swaps two nodes at indices 'i' and 'j'."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
