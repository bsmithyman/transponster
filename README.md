transponster
============

Tracks visitors by IP and plots on a map; solves heat equation.

<dl>
  <dt>common.py</dt>
  <dd>Contains database and format conversion code.</dd>

  <dt>heateqn.py</dt>
  <dd>Script to time-step the model and add new perturbations. The script code accesses the MongoDB
      instance to pull out model and IP log information. It then calls `perturb` to add a unit
      perturbation to the model at each extracted lat/long position. Finally, a single explicit time
      step is triggered by calling `disperse`.
  </dd>
  
  <dt>initialize.py</dt>
  <dd>Script to (re)create the model and initialize it to zero.</dd>
  
  <dt>transponster.py</dt>
  <dd>Flask app to handle the server-side aspects. Specifically set up to run on Heroku (behind a
      proxy), but it would be straightforward to remove this limitation. Accessing the server root
      causes a call to the hostip.info API, which ideally returns a JSON package containing the
      latitude and longditude of the user. This then triggers a redirect to `/index`, which returns
      simple static HTML. The image tag on the index page triggers a load of `/render.png`, which
      is served by the `render` function. This pulls the model out of the database and converts it
      to a PNG image.
  </dd>
</dl>
