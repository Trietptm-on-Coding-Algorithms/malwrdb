import { Component, OnInit, Input } from '@angular/core';

import { Sample } from '../../models/models';
import { ServerDataService } from '../../services/server-data.service';

@Component({
  selector: 'sample',
  template: `
    <p>
        {{ sample.md5 }}
    </p>
  `
})

export class SampleComponent implements OnInit {
  @Input() sample: Sample;
  constructor(private _svrdata: ServerDataService) { }

  ngOnInit() {
    // get data from server
  }
}
