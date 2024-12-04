package com.example.service;

import com.example.model.StockRecord;
import java.util.List;
import java.util.Optional;

public interface StockRecordService {
    List<StockRecord> getAllStockRecords();  // Метод за враќање на сите записи
    Optional<StockRecord> getStockRecordById(Long id);  // Метод за враќање на запис според ID
    StockRecord saveStockRecord(StockRecord stockRecord);  // Метод за спасување или ажурирање на запис
    void deleteStockRecord(Long id);  // Метод за бришење на запис

    // Нов метод што ќе го додадеме:
    List<StockRecord> findAllByStockCode(String stockCode);  // Метод за пребарување записи според stockCode
}
