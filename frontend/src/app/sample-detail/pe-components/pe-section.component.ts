import { Component, OnInit, Input } from '@angular/core';

import { MaterialComponentModule } from '../../modules/material-component.module';

import { PeSample } from '../../models/models-pe';
import { ServerDataService } from '../../services/server-data.service';


@Component({
  selector: 'pe-section',
  template: `
  <h1>Pe Section</h1>
  `,
})
export class PeSectionComponent implements OnInit {
  @Input() peSample: PeSample;

  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // this._svrdata.get();
  }
}
