public class Payment {
    boolean charge(String userId, double amount) {
        return true;
    }

    void refund(String userId, double amount) {
        System.out.println("Refunded " + amount);
    }
}
