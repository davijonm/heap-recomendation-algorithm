import heapq
from threading import Lock

class TrendyProductRecommender:
    def __init__(self):
        # Initialize a dictionary to track clicks for each product
        self.click_counts = {}
        # A min-heap to store the top 10 products by clicks
        self.top_10_heap = []
        # Lock for thread-safe operations
        self.lock = Lock()

    def record_click(self, product_id):
        """
        Records a click for a given product.
        :param product_id: The unique identifier of the product that was clicked.
        """
        with self.lock:
            # Increment the click count for the product
            if product_id in self.click_counts:
                self.click_counts[product_id] += 1
            else:
                self.click_counts[product_id] = 1

            # Update the min-heap
            heapq.heappush(self.top_10_heap, (self.click_counts[product_id], product_id))

            # Remove excess elements to keep only the top 10
            if len(self.top_10_heap) > 10:
                heapq.heappop(self.top_10_heap)

            # Rebuild the heap to ensure the top 10 are accurate
            self.top_10_heap = heapq.nlargest(10, self.top_10_heap, key=lambda x: (x[0], x[1]))
            heapq.heapify(self.top_10_heap)

    def get_top_10_clicked_products(self):
        """
        Retrieves the top 10 products based on the number of clicks.
        :return: A list of tuples with product ID and click count,
                 sorted in descending order of clicks.
        """
        with self.lock:
            # lock ensure thread safety. This means that the code block within this statement is executed while holding a lock, preventing other threads from modifying self.top_10_heap concurrently. This is crucial in a multi-threaded environment to avoid race conditions and ensure data consistency.
            # Convert the heap into a sorted list in descending order
            return sorted(self.top_10_heap, key=lambda x: (-x[0], x[1]))


def test_recommender():
    recommender = TrendyProductRecommender()

    clicks = [101, 102, 103, 103]

    for i, product_id in enumerate(clicks):
        print(f"\nClick {i+1}: Product {product_id}")
        recommender.record_click(product_id)

        # Show the current state of recorded clicks
        print("Clicks count:", recommender.click_counts)

        # Show the current state of the top 10 products heap (not ordered)
        print("Top 10 heap (not ordered):", recommender.top_10_heap)

        # Show the top 10 most clicked products
        top_10 = recommender.get_top_10_clicked_products()
        print("Top 10 products clicked", top_10)


test_recommender()
