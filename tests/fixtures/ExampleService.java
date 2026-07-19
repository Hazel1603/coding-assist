package tests.fixtures;

import java.util.Optional;

public class ExampleService {
    private final UserRepository userRepository;

    public ExampleService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public String findDisplayName(long userId) {
        Optional<User> user = userRepository.findById(userId);

        if (user.isEmpty()) {
            return "Unknown user";
        }

        User foundUser = user.get();
        return foundUser.firstName() + " " + foundUser.lastName();
    }

    public interface UserRepository {
        Optional<User> findById(long userId);
    }

    public record User(String firstName, String lastName) {}
}
