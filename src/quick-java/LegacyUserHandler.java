import java.util.*;

public class LegacyUserHandler {

    public static class User {
        public String name;
        public int id;
    }

    private static int MAX_USERS = 100;
    private static List<User> database = new ArrayList<>();

    public User findUser(String name) {
        try {
            for (User u : database) {
                if (u.name.equals(name)) {
                    return u;
                }
            }

            throw new Exception("User not found");
        } catch (Exception e) {

            System.out.println("Error: " + e.getMessage());
            return null;
        }
    }

    public synchronized void slowProcess(User u) {

        new Thread(() -> {
            System.out.println("Processing " + u.name);
        }).start();
    }
}