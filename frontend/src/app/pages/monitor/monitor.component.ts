import { AfterContentInit, AfterViewInit, Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
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


@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.scss']
})
export class MonitorComponent implements OnInit, AfterViewInit {

  constructor(private monitor: MonitorService, private dialog: MatDialog, private snackbar: MatSnackBar) { }

  sendRequestForm = new FormGroup({
    tasks: new FormArray([], [ArrayLenghtValidator({ min: 1})]),
  });

  @ViewChild('container') container!: ElementRef<HTMLInputElement>;

  rowHeigth: number = 0;

  vmData!: VmDataMap;
  configureDialogRef!: MatDialogRef<ConfigureComponent> | null;
  vmDataSubscription!: Subscription;
  vmDataArray: any[] = [];

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
    })
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

  configure() {
    this.configureDialogRef = this.dialog.open(ConfigureComponent);

    this.configureDialogRef.afterClosed().subscribe(result => {
      this.configureDialogRef = null;
    });
  }

  computeArray() {
    this.vmDataArray = Object.entries(this.vmData).map(([name, vmData]) => {
      return { name, value: vmData.percentage || 1 };
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

}
