package com.example;
import java.util.List;
public class Order {
    private List<Item> items;
    public Order(List<Item> items){ this.items=items; }
    public List<Item> getItems(){ return items; }
}
