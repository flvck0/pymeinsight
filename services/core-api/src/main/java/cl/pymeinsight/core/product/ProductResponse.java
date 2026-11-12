package cl.pymeinsight.core.product;

public record ProductResponse(
        Long id,
        String sku,
        String name,
        int stock,
        int minStock,
        int priceClp,
        boolean lowStock) {

    public static ProductResponse from(Product p) {
        return new ProductResponse(
                p.getId(), p.getSku(), p.getName(),
                p.getStock(), p.getMinStock(), p.getPriceClp(),
                p.getStock() <= p.getMinStock());
    }
}
