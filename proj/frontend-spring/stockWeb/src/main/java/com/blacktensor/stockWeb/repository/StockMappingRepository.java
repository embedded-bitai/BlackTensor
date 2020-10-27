package com.blacktensor.stockWeb.repository;

import com.blacktensor.stockWeb.entity.StockMapping;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StockMappingRepository extends JpaRepository<StockMapping, Long> {
    List<StockMapping> findByStockName(String stockName);
}
