import { Component, ViewChild } from '@angular/core';
import { ServerDataService } from '../services/server-data.service'

import { ContextMenuModule, ContextMenuComponent } from 'ngx-contextmenu';

@Component({
  selector: 'test',
  template: `
  <ul>
      <li *ngFor="let item of items" [contextMenu]="basicMenu" [contextMenuSubject]="item">Right Click: {{item?.name}}</li>
  </ul>
  <context-menu>
    <ng-template contextMenuItem (execute)="showMessage('Hi, ' + $event.item.name)">
      Say hi!
    </ng-template>

    <ng-template contextMenuItem divider="true"></ng-template>

    <ng-template contextMenuItem let-item (execute)="showMessage($event.item.name + ' said: ' + $event.item.otherProperty)">
      Bye, {{item?.name}}
    </ng-template>

    <ng-template contextMenuItem passive="true">
      Input something: <input type="text">
    </ng-template>

  </context-menu>
  `,
  styleUrls: ['./test.component.css']
})
export class TestComponent{

  constructor(private _dtctx: ServerDataService) { }

  public items = [
    { name: 'John', otherProperty: 'Foo' },
    { name: 'Joe', otherProperty: 'Bar' }
  ];
  @ViewChild(ContextMenuComponent) public basicMenu: ContextMenuComponent;

  showMessage(arg: any){
    console.log(arg);
  }

}
