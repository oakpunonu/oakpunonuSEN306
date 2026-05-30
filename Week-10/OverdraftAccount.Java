public class OverdraftAccount extends BankAccount {

    public OverdraftAccount(double balance) {
        super(balance);
    }

    @Override
    public void withdraw(double amount) {

        if (balance - amount >= -500) {

            balance -= amount;

            System.out.println("Withdrawn: " + amount);
            System.out.println("New balance: " + balance);

        } else {
            System.out.println("Overdraft limit exceeded");
        }
    }
}