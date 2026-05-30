public class Shipping {
    String createLabel(String address) {
        return "TRK" + System.currentTimeMillis();
    }

    void schedulePickup(String label) {
        System.out.println("Pickup scheduled: " + label);
    }

    boolean isAvailable() {
        return true;
    }
}
