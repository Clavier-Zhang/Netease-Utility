package cloud.model.user;

import org.springframework.data.repository.CrudRepository;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


public interface UserRepository extends CrudRepository<User, Long> {

    List<User> findAllByIdGreaterThanEqualAndIdLessThanEqual(long start, long end);

    List<User> findAllByIdGreaterThanEqualAndIdLessThanEqualAndGender(long start, long end, int gender);

    List<User> findTop100BySearchedFalseOrderByIdAsc();

    List<User> findTop100BySearchedFalseOrderByIdDesc();

}