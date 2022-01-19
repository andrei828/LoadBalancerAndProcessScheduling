import { AfterContentInit, AfterViewChecked, AfterViewInit, Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
import { FormArray, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { interval, Subscription } from 'rxjs';
import { ConfigureComponent } from 'src/app/components/configure/configure.component';
import { VmDataMap } from 'src/app/lib/model/VmDataMap';
import { MonitorService } from 'src/app/services/monitor.service';
import { startWith, switchMap } from 'rxjs/operators';
import { Request } from 'src/app/lib/model/Request';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ArrayLenghtValidator } from 'src/app/lib/validators/ArrayLengthValidator';
import { Log } from 'src/app/lib/model/Log';
import { getMaxScrollTop, groupBy } from 'src/app/lib/util';
import { RandomTasksComponent } from 'src/app/components/random-tasks/random-tasks.component';
import { Task } from 'src/app/lib/model/Task';


@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.scss']
})
export class MonitorComponent implements OnInit, AfterViewInit, AfterViewChecked {

  constructor(private monitor: MonitorService, private dialog: MatDialog, private snackbar: MatSnackBar) { }

  sendRequestForm = new FormGroup({
    tasks: new FormArray([], [ArrayLenghtValidator({ min: 1})]),
  });

  @ViewChild('container') container!: ElementRef<HTMLInputElement>;
  @ViewChild('logsContainer') logsContainer!: ElementRef<HTMLInputElement>;

  rowHeigth: number = 0;

  vmData!: VmDataMap;
  configureDialogRef!: MatDialogRef<ConfigureComponent> | null;
  vmDataSubscription!: Subscription;
  vmDataArray: any[] = [];

  logs: Log[] = [
    // {
    //   "content": "Starting virtual machine [Thread-3]...",
    //   "from": "VM-Thread-3",
    //   "level": "INFO",
    //   "timestamp": "2022-01-19 15:16:06.490953"
    // },
  ];
  groupedLogs: { [name: string]: Log[] } = {};
  selectedLogsArray: Log[] = this.logs;
  logSubscription!: Subscription;

  selectedLogsFrom = new FormControl(null);
  logsFromOptions: string[] = [];


  ngOnInit(): void {
    this.vmDataSubscription = interval(1000)
    .pipe(
      switchMap(_ => this.monitor.getVmData())
    ).subscribe(result => {
      this.vmData = result;
      if(!result && !this.configureDialogRef) {
        this.configure();
      }
      if(result) {
        this.computeArray();
      }
    });

    this.logSubscription = interval(1000)
      .pipe(switchMap(_ => this.monitor.getLogs()))
      .subscribe(logs => {
        this.logs = this.logs.concat(logs);
        this.computeGroupedLogs();
      });
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.onResize();
    }, 0);
  }

  ngAfterViewChecked(): void {
    this.scrollLogsContainer();
  }

  computeGroupedLogs() {
    this.groupedLogs = groupBy(this.logs, (log) => log.from);
    this.logsFromOptions = Object.keys(this.groupedLogs).sort();
    const selected = this.selectedLogsFrom.value;
    if(!selected) {
      this.selectedLogsArray = this.logs;
    } else {
      this.selectedLogsArray = this.groupedLogs[selected];
    }
    this.scrollLogsContainer();
  }

  scrollLogsContainer() {
    let el = this.logsContainer.nativeElement;
    if(el.scrollTop < getMaxScrollTop(el)) return;
    try {
      this.logsContainer.nativeElement.scrollTop = this.logsContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.rowHeigth = this.container.nativeElement.clientHeight / 2;
  }

  get taskFormArray() {
    return this.sendRequestForm.get("tasks") as FormArray;
  }

  get totalTasks() {
    return this.taskFormArray.controls.length;
  }

  addTask(from?: Task) {
    const task = new FormGroup({
      duration: new FormControl(from?.duration, [Validators.required])
    });
    this.taskFormArray.insert(0, task);
  }

  configure() {
    this.configureDialogRef = this.dialog.open(ConfigureComponent);

    this.configureDialogRef.afterClosed().subscribe(result => {
      this.configureDialogRef = null;

      if(result) {
        this.logs = [];
        this.selectedLogsFrom.setValue(null);
        this.computeGroupedLogs();
      }
    });
  }

  computeArray() {
    this.vmDataArray = Object.entries(this.vmData).map(([name, vmData]) => {
      return { name, value: vmData.percentage || 0.5 };
    });
  }

  sendRequest() {
    const request = this.sendRequestForm.value as Request;
    this.monitor.sendRequest(request).subscribe(result => {
      if(result) {
        this.vmData = result;
        this.computeArray();
        this.snackbar.open("Request sent.");
        this.sendRequestForm = new FormGroup({
          tasks: new FormArray([], [ArrayLenghtValidator({ min: 1})]),
        });
      }
    });
  }

  openRandomDialog() {
    let dialogRef = this.dialog.open<RandomTasksComponent, any, Task[]>(RandomTasksComponent);

    dialogRef.afterClosed().subscribe(result => {
      if(result) {
        this.sendRequestForm = new FormGroup({
          tasks: new FormArray([], [ArrayLenghtValidator({ min: 1})]),
        });
        result.forEach(task => this.addTask(task));
      }
    });
  }

}
