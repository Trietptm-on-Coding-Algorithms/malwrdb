import { Component, ViewChild, OnInit, Input } from '@angular/core';

import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

import { Sample } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

@Component({
  selector: 'sample',
  template: `
    <a href="" style="background-color: yellow" [contextMenu]="basicMenu">{{ sample.sample_name }}</a>

    <!-- RightClick menu to select actions -->
    <context-menu>
      <ng-template contextMenuItem (execute)="convertToRefFile()">Convert to reference file!</ng-template>
      <ng-template contextMenuItem (execute)="renameSample()">Rename</ng-template>
      <ng-template contextMenuItem (execute)="delSample()">Delete</ng-template>
    </context-menu>
  `
})

export class SampleComponent implements OnInit {
  @Input() sample: Sample;
    @ViewChild(ContextMenuComponent) basicMenu: ContextMenuComponent;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // get data from server
  }
    convertToRefFile() {
        console.log("convert sample to file");
    }

    renameSample() {
        console.log("rename sample");
    }

    delSample() {
        console.log("del sample");
    }
}
