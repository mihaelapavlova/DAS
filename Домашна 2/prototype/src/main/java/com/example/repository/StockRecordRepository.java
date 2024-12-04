package com.example.repository;

import com.example.model.StockRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface StockRecordRepository extends JpaRepository<StockRecord, Long> {
    List<StockRecord> findByStockCode(String stockCode);  
}
