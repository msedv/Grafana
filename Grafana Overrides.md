We have a bunch of sensors (e.g. 25-30 ESPs running Tasmota) sending different measurements to MQTT - Influx - Grafana; works real nice. In the legend in the moment the ID of the devices is displayed:

![GrafanaOverrides1](https://user-images.githubusercontent.com/7942032/153693925-8a8c5482-2929-4fbf-b1c9-5a6787cce99b.png)
![GrafanaOverrides2](https://user-images.githubusercontent.com/7942032/153693926-11479822-3616-48e1-b715-c1b51bbbaebb.png)

My end users would like to see a more human readable description like "machine x/hall y" instead of "DF6B09". Of course I could to the lookup on the import side but that would store a lot of redundant text for millions of measurements and arises problems if one of the descriptions will change (which for sure will be happen…).

In the [Grafana community](https://community.grafana.com/t/lookup-of-device-ids-for-legend/60401) Grant Pinkos made the suggestion to use overlays to get a more descriptive legend.

On the options tab right of the graph per default "All" is selected:

![GrafanaOverrides3](https://user-images.githubusercontent.com/7942032/153693927-74772f5d-40a0-4b6f-a886-8e454264ea44.png)

Switching to "Overrides":

![GrafanaOverrides4](https://user-images.githubusercontent.com/7942032/153693928-1d6bc897-ddf1-411a-a903-6238a21e9ee8.png)

allows us to add a field override; we choose "Fields with name":

![GrafanaOverrides5](https://user-images.githubusercontent.com/7942032/153693929-1baadade-5257-4d44-a32c-d98037e3f967.png)

Select the field which should be replaced:

![GrafanaOverrides6](https://user-images.githubusercontent.com/7942032/153693930-bd021491-79eb-4a25-b81f-01e84dcf14ef.png)

We want to change the display name (hint: typing "dis" reduces the many possible options):

![GrafanaOverrides7](https://user-images.githubusercontent.com/7942032/153694156-8aadfac0-bfcb-4a1d-a178-73625633a27a.png)

And give it a nice description:

![GrafanaOverrides8](https://user-images.githubusercontent.com/7942032/153693936-c69939e2-6737-43a3-9ad7-7ce99f411c24.png)

A view other overrides:

![GrafanaOverrides9](https://user-images.githubusercontent.com/7942032/153693938-f839f4df-243f-45e0-8bd6-8694875c1656.png)

And the result:

![GrafanaOverrides10](https://user-images.githubusercontent.com/7942032/153693939-27e48370-f7b7-4fcf-8391-52632851dd2f.png)

Of course it would be a real burden to do that manually in many dashboards/panels for dozens of sensors - particularly because I could to all the mappings automatically. So I digged "a little bit" into the Grafanas data structures and made a [proof of concept ython-script](https://github.com/msedv/Grafana/blob/main/parsegrafana.py) which I could/would extend to automize the process of defining the overrides.
