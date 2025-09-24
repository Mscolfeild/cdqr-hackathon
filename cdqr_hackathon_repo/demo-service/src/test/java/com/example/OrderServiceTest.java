package com.example;
import org.junit.jupiter.api.Test;
import java.util.Arrays;
import static org.junit.jupiter.api.Assertions.*;

class OrderServiceTest {
    @Test void calculatesTotal() {
        OrderService s=new OrderService();
        Order o=new Order(Arrays.asList(new Item(10),new Item(20)));
        assertEquals(30,s.calculateTotal(o));
    }
}
