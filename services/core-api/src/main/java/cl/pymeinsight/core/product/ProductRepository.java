package cl.pymeinsight.core.product;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface ProductRepository extends JpaRepository<Product, Long> {

    @Query("select p from Product p where p.stock <= p.minStock order by p.stock asc")
    List<Product> findLowStock();
}
