package cl.pymeinsight.core.product;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ProductRequest(
        @NotBlank @Size(max = 40) String sku,
        @NotBlank @Size(max = 120) String name,
        @Min(0) int stock,
        @Min(0) int minStock,
        @Min(0) int priceClp) {
}
