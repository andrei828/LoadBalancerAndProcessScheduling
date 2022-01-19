import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Task } from 'src/app/lib/model/Task';
import { randomBetween, randomIntBetween } from 'src/app/lib/util';

@Component({
  selector: 'app-random-tasks',
  templateUrl: './random-tasks.component.html',
  styleUrls: ['./random-tasks.component.scss']
})
export class RandomTasksComponent implements OnInit {

  constructor(private dialogRef: MatDialogRef<RandomTasksComponent>) { }


  randomForm = new FormGroup({
    minTaskNumber: new FormControl(null, [Validators.required, Validators.min(1)]),
    maxTaskNumber: new FormControl(null, [Validators.required, Validators.min(1)]),
    minTaskDuration: new FormControl(null, [Validators.required, Validators.min(1)]),
    maxTaskDuration: new FormControl(null, [Validators.required, Validators.min(1)]),
  });

  ngOnInit(): void {
  }

  generate() {
    const value = this.randomForm.value;
    const taskNumber = randomIntBetween(value.minTaskNumber, value.maxTaskNumber);
    const tasks: Task[] = Array.from(Array(taskNumber))
      .map(_ => ({ duration: randomIntBetween(value.minTaskDuration, value.maxTaskDuration)}));
    
    this.dialogRef.close(tasks);
  }

}
