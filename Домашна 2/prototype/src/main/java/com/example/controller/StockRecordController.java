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
@CrossOrigin(origins = "*")  // Овозможува пристап од било кој домен
public class StockRecordController {

    private final StockRecordService stockRecordService;

    @Autowired
    public StockRecordController(StockRecordService stockRecordService) {
        this.stockRecordService = stockRecordService;  // Инициализирање на сервисот
    }

    // Ендпоинт за враќање на сите записи
    @GetMapping(value = "/all")
    public ResponseEntity<List<StockRecord>> getAllStockRecords() {
        List<StockRecord> stockRecords = stockRecordService.getAllStockRecords();
        return new ResponseEntity<>(stockRecords, HttpStatus.OK);  // Враќа сите записи со 200 OK статус
    }

    // Ендпоинт за враќање на конкретен запис според ID
    @GetMapping(value = "/stock-records/{id}")
    public ResponseEntity<StockRecord> getStockRecordById(@PathVariable(value = "id") Long id) {
        Optional<StockRecord> stockRecord = stockRecordService.getStockRecordById(id);
        return stockRecord.map(record -> new ResponseEntity<>(record, HttpStatus.OK))  // Враќа 200 OK со записот
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));  // Ако не е најдено, враќа 404 Not Found
    }

    // Ендпоинт за додавање на нов запис
    @PostMapping(value = "/stock-records")
    public ResponseEntity<StockRecord> createStockRecord(@RequestBody StockRecord stockRecord) {
        StockRecord createdRecord = stockRecordService.saveStockRecord(stockRecord);
        return new ResponseEntity<>(createdRecord, HttpStatus.CREATED);  // Враќа 201 Created со новиот запис
    }

    // Ендпоинт за ажурирање на постоечки запис
    @PutMapping(value = "/stock-records/{id}")
    public ResponseEntity<StockRecord> updateStockRecord(@PathVariable(value = "id") Long id, @RequestBody StockRecord stockRecord) {
        Optional<StockRecord> existingRecord = stockRecordService.getStockRecordById(id);
        if (existingRecord.isPresent()) {
            stockRecord.setId(id);  // Осигурајте се дека ID-то е точно при ажурирањето
            StockRecord updatedRecord = stockRecordService.saveStockRecord(stockRecord);
            return new ResponseEntity<>(updatedRecord, HttpStatus.OK);  // Враќа 200 OK со ажурираниот запис
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);  // Враќа 404 ако записот не е најден
    }

    // Ендпоинт за бришење на запис
    @DeleteMapping(value = "/stock-records/{id}")
    public ResponseEntity<Void> deleteStockRecord(@PathVariable(value = "id") Long id) {
        Optional<StockRecord> stockRecord = stockRecordService.getStockRecordById(id);
        if (stockRecord.isPresent()) {
            stockRecordService.deleteStockRecord(id);
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);  // Враќа 204 No Content по успешно бришење
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);  // Враќа 404 ако записот не е најден
    }

    // Ендпоинт за пребарување на записи според stockCode
    @GetMapping(value = "/stock-records/stock-code/{stockCode}")
    public ResponseEntity<List<StockRecord>> getStockRecordsByStockCode(@PathVariable(value = "stockCode") String stockCode) {
        List<StockRecord> records = stockRecordService.findAllByStockCode(stockCode);
        if (records.isEmpty()) {
            return new ResponseEntity<>(HttpStatus.NO_CONTENT);  // Враќа 204 ако нема записи
        }
        return new ResponseEntity<>(records, HttpStatus.OK);  // Враќа 200 OK со резултатите
    }
}
