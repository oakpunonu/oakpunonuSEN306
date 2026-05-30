public class Main {

    public static void main(String[] args) {

        // Exercise 1 Testing
        QueueADT q = new LinkedQueue();

        q.enqueue(10);
        q.enqueue(20);
        q.enqueue(30);

        System.out.println(q.dequeue());
        System.out.println(q.size());
        System.out.println(q.isEmpty());

        // Exercise 2 Testing
        OverdraftAccount acc = new OverdraftAccount(100);

        acc.withdraw(200);
        acc.withdraw(300);
        acc.withdraw(200);

        System.out.println("Final Balance: " + acc.getBalance());
    }
}