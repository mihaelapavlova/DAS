package com.example.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.*;

import java.io.Serializable;
import java.time.LocalDate;

@Data
@Entity
@Table(name = "stock_records")
@NoArgsConstructor
@AllArgsConstructor
public class StockRecord implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotEmpty
    @Column(name = "stock_code", nullable = false)
    private String stockCode;

    @NotNull
    @Column(name = "date", nullable = false)
    private LocalDate date;

    @Positive
    @Column(name = "last_transaction_price")
    private Double lastTransactionPrice;

    @Positive
    @Column(name = "quantity")
    private Integer quantity;

    @Column(name = "percentage_change")
    private Double percentageChange;

    @Column(name = "total_turnover")
    private Double totalTurnover;

    @NotEmpty
    @Column(name = "description")
    private String description;

    @NotNull
    @Column(name = "unique_identifier", unique = true, nullable = false)
    private String uniqueIdentifier;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getStockCode() {
        return stockCode;
    }

    public void setStockCode(String stockCode) {
        this.stockCode = stockCode;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Double getLastTransactionPrice() {
        return lastTransactionPrice;
    }

    public void setLastTransactionPrice(Double lastTransactionPrice) {
        this.lastTransactionPrice = lastTransactionPrice;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    public Double getPercentageChange() {
        return percentageChange;
    }

    public void setPercentageChange(Double percentageChange) {
        this.percentageChange = percentageChange;
    }

    public Double getTotalTurnover() {
        return totalTurnover;
    }

    public void setTotalTurnover(Double totalTurnover) {
        this.totalTurnover = totalTurnover;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getUniqueIdentifier() {
        return uniqueIdentifier;
    }

    public void setUniqueIdentifier(String uniqueIdentifier) {
        this.uniqueIdentifier = uniqueIdentifier;
    }
}
