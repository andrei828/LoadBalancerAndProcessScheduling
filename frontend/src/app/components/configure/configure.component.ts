import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { MonitorService } from 'src/app/services/monitor.service';

@Component({
  selector: 'app-configure',
  templateUrl: './configure.component.html',
  styleUrls: ['./configure.component.scss']
})
export class ConfigureComponent implements OnInit {

  constructor(private dialogRef: MatDialogRef<ConfigureComponent>, private monitor: MonitorService) { }

  configureForm = new FormGroup({
    vmNumber: new FormControl(null, [Validators.required, Validators.min(1)])
  });

  ngOnInit(): void {
  }

  configure() {
    this.monitor.configure(this.configureForm.get("vmNumber")?.value).subscribe(result => {
      if(result) {
        this.dialogRef.close(true);
      }
    })
  }

}
