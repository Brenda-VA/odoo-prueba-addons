import {Component} from "@odoo/owl";

export class Counter extends Component {
    static template = "owl_course.Counter";

    setup() {
        this.state = useState({ count: 0, history: [] });
    }

    increment() {
        this.count++;
        this.state.history.push({
            
        });
    }

    decrement() {
        this.count--;
        this.state.history.push(this.count);
    }
}