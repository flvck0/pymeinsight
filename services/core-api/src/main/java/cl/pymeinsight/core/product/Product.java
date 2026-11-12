package cl.pymeinsight.core.product;

import jakarta.persistence.*;
import java.time.OffsetDateTime;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 40)
    private String sku;

    @Column(nullable = false, length = 120)
    private String name;

    @Column(nullable = false)
    private int stock;

    @Column(name = "min_stock", nullable = false)
    private int minStock;

    @Column(name = "price_clp", nullable = false)
    private int priceClp;

    @Column(name = "created_at", nullable = false, insertable = false, updatable = false)
    private OffsetDateTime createdAt;

    protected Product() {
    }

    public Product(String sku, String name, int stock, int minStock, int priceClp) {
        this.sku = sku;
        this.name = name;
        this.stock = stock;
        this.minStock = minStock;
        this.priceClp = priceClp;
    }

    public void update(String sku, String name, int stock, int minStock, int priceClp) {
        this.sku = sku;
        this.name = name;
        this.stock = stock;
        this.minStock = minStock;
        this.priceClp = priceClp;
    }

    public Long getId() { return id; }
    public String getSku() { return sku; }
    public String getName() { return name; }
    public int getStock() { return stock; }
    public int getMinStock() { return minStock; }
    public int getPriceClp() { return priceClp; }
    public OffsetDateTime getCreatedAt() { return createdAt; }
}
