package com.example.controller;

import com.example.model.StockRecord;
import com.example.service.StockRecordService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping(value = "/api")
@Validated
@CrossOrigin(origins = "*")  
public class StockRecordController {

    private final StockRecordService stockRecordService;

    @Autowired
    public StockRecordController(StockRecordService stockRecordService) {
        this.stockRecordService = stockRecordService; 
    }

    @GetMapping(value = "/all")
    public ResponseEntity<List<StockRecord>> getAllStockRecords() {
        List<StockRecord> stockRecords = stockRecordService.getAllStockRecords();
        return new ResponseEntity<>(stockRecords, HttpStatus.OK);  
    }

    
    @GetMapping(value = "/stock-records/{id}")
    public ResponseEntity<StockRecord> getStockRecordById(@PathVariable(value = "id") Long id) {
        Optional<StockRecord> stockRecord = stockRecordService.getStockRecordById(id);
        return stockRecord.map(record -> new ResponseEntity<>(record, HttpStatus.OK)) 
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND)); 
    }

    @PostMapping(value = "/stock-records")
    public ResponseEntity<StockRecord> createStockRecord(@RequestBody StockRecord stockRecord) {
        StockRecord createdRecord = stockRecordService.saveStockRecord(stockRecord);
        return new ResponseEntity<>(createdRecord, HttpStatus.CREATED);  
    }

    @PutMapping(value = "/stock-records/{id}")
    public ResponseEntity<StockRecord> updateStockRecord(@PathVariable(value = "id") Long id, @RequestBody StockRecord stockRecord) {
        Optional<StockRecord> existingRecord = stockRecordService.getStockRecordById(id);
        if (existingRecord.isPresent()) {
            stockRecord.setId(id); 
            StockRecord updatedRecord = stockRecordService.saveStockRecord(stockRecord);
            return new ResponseEntity<>(updatedRecord, HttpStatus.OK); 
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND); 
    }
    
    @DeleteMapping(value = "/stock-records/{id}")
    public ResponseEntity<Void> deleteStockRecord(@PathVariable(value = "id") Long id) {
        Optional<StockRecord> stockRecord = stockRecordService.getStockRecordById(id);
        if (stockRecord.isPresent()) {
            stockRecordService.deleteStockRecord(id);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);  
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND); 
    }

  
    @GetMapping(value = "/stock-records/stock-code/{stockCode}")
    public ResponseEntity<List<StockRecord>> getStockRecordsByStockCode(@PathVariable(value = "stockCode") String stockCode) {
        List<StockRecord> records = stockRecordService.findAllByStockCode(stockCode);
        if (records.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);  
        }
        return new ResponseEntity<>(records, HttpStatus.OK); 
    }
}
