/*
Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import { Component, Input } from '@angular/core';

@Component({
  selector: 'mcrb-severity',
  templateUrl: './severity.component.html',
  styleUrls: ['./severity.component.scss']
})
export class SeverityComponent {
  @Input() severityLevel: string = 'high';
  get color(): string {
    switch (this.severityLevel) {
      case 'critical':
        return 'accent'
      case 'error':
        return 'warn'
      default:
        return 'primary';
    }
  }

  get icon(): string {
    switch (this.severityLevel) {
      case 'critical':
        return 'warning'
      case 'error':
        return 'warning'
      default:
        return 'info';
    }

  }

}
