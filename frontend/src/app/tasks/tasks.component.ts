import { Component, OnInit, Input } from '@angular/core';

import { Task } from '../models/models';
import { ServerDataService } from '../services/server-data.service';

import { MaterialComponentModule } from '../modules/material-component.module';

@Component({
  selector: 'task-list',
  template: `
  <h1>Tasks</h1>
  <button mat-raised-button color="primary" (click)="test($event)">Test It</button>
  `
})

export class TaskListComponent implements OnInit {
  taskList: Task[];

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // this._svrdata.getTaskList().subscribe(
    //   v => {
    //     this.taskList = v;
    //   },
    //   e => {
    //     console.log("getTaskList fail: " + e);
    //   }
    // );
  }

  test(evt: any){
    this._svrdata.cmdTest();
  }

}
