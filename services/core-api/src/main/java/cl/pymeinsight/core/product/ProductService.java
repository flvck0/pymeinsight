package cl.pymeinsight.core.product;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
@Transactional
public class ProductService {

    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> list() {
        return repository.findAll().stream().map(ProductResponse::from).toList();
    }

    @Transactional(readOnly = true)
    public List<ProductResponse> lowStock() {
        return repository.findLowStock().stream().map(ProductResponse::from).toList();
    }

    public ProductResponse create(ProductRequest r) {
        Product saved = repository.save(
                new Product(r.sku(), r.name(), r.stock(), r.minStock(), r.priceClp()));
        return ProductResponse.from(saved);
    }

    public ProductResponse update(Long id, ProductRequest r) {
        Product p = find(id);
        p.update(r.sku(), r.name(), r.stock(), r.minStock(), r.priceClp());
        return ProductResponse.from(p);
    }

    public void delete(Long id) {
        repository.delete(find(id));
    }

    private Product find(Long id) {
        return repository.findById(id).orElseThrow(() ->
                new ResponseStatusException(HttpStatus.NOT_FOUND, "Producto no encontrado: " + id));
    }
}
