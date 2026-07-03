import { Component } from "@odoo/owl";

export class Counter extends Component {
    static template = "owl_course.Counter";

    setup() {
        this.state = userState({ count: 0, history: [] });
        this.count = 0;
    }

    increment() {
        this.count++;
        this.state.history.push({ 
            action: "increment", 
            value: this.count, 
            timestamp: new Date().toLocaleTimeString() 
        });
    }

    decrement() {
        this.count--;
        this.state.history.push({ 
            action: "decrement", 
            value: this.count, 
            timestamp: new Date().toLocaleTimeString()
        });
    }

    reset() {
        this.count = 0;
        this.state.history = [];
    }

}