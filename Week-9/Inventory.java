public class Inventory {
    boolean checkStock(String productId) {
        return true;
    }

    void reserve(String productId) {
        System.out.println("Reserved " + productId);
    }

    void release(String productId) {
        System.out.println("Released " + productId);
    }
}
