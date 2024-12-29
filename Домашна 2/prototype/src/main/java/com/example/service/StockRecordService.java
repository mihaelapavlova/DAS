package com.example.service;

import com.example.model.StockRecord;
import java.util.List;
import java.util.Optional;

public interface StockRecordService {
    List<StockRecord> getAllStockRecords();  
    Optional<StockRecord> getStockRecordById(Long id); 
    StockRecord saveStockRecord(StockRecord stockRecord);  
    void deleteStockRecord(Long id);  
    
    List<StockRecord> findAllByStockCode(String stockCode);  
}
