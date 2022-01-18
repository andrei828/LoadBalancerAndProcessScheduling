import { AfterContentInit, AfterViewInit, Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.scss']
})
export class MonitorComponent implements OnInit, AfterViewInit {

  constructor() { }

  sendRequestForm = new FormGroup({
    tasks: new FormArray([]),
  });

  @ViewChild('container') container!: ElementRef<HTMLInputElement>;

  rowHeigth: number = 0;

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.onResize();
    }, 0);
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.rowHeigth = this.container.nativeElement.clientHeight / 2;
  }

  get taskFormArray() {
    return this.sendRequestForm.get("tasks") as FormArray;
  }

  addTask() {
    const task = new FormGroup({
      duration: new FormControl(null, [Validators.required])
    });
    this.taskFormArray.push(task);
  }

  

}
