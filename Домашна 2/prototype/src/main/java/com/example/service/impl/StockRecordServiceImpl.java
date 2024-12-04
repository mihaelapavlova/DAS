package com.example.service.impl;

import com.example.model.StockRecord;
import com.example.repository.StockRecordRepository;
import com.example.service.StockRecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class StockRecordServiceImpl implements StockRecordService {

    private final StockRecordRepository stockRecordRepository;

    @Autowired
    public StockRecordServiceImpl(StockRecordRepository stockRecordRepository) {
        this.stockRecordRepository = stockRecordRepository;  // Инициализација на repository
    }

    @Override
    public List<StockRecord> getAllStockRecords() {
        return stockRecordRepository.findAll();  // Враќа сите записи од базата
    }

    @Override
    public Optional<StockRecord> getStockRecordById(Long id) {
        return stockRecordRepository.findById(id);  // Враќа запис според ID
    }

    @Override
    public StockRecord saveStockRecord(StockRecord stockRecord) {
        return stockRecordRepository.save(stockRecord);  // Спасува или ажурира запис
    }

    @Override
    public void deleteStockRecord(Long id) {
        stockRecordRepository.deleteById(id);  // Брише запис според ID
    }

    @Override
    public List<StockRecord> findAllByStockCode(String stockCode) {
        return stockRecordRepository.findByStockCode(stockCode);  // Пребарува записи според stockCode
    }
}
