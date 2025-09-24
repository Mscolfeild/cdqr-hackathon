package com.example;
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    public int calculateTotal(Order order) {
        return order.getItems().stream()
            .mapToInt(Item::getPrice)
            .sum(); // order null olursa hata verir!
    }
}
