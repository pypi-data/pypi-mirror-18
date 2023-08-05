TestHelpers.commonWidgetTests( "sortable", {
	defaults: {
		appendTo: "parent",
		axis: false,
		cancel: "input,textarea,button,select,option",
		connectWith: false,
		containment: false,
		cursor: "auto",
		cursorAt: false,
		delay: 0,
		disabled: false,
		distance: 1,
		dropOnEmpty: true,
		forcePlaceholderSize: false,
		forceHelperSize: false,
		grid: false,
		handle: false,
		helper: "original",
		items: "> *",
		opacity: false,
		placeholder: false,
		revert: false,
		scroll: true,
		scrollSensitivity: 20,
		scrollSpeed: 20,
		scope: "default",
		tolerance: "intersect",
		zIndex: 1000,

		// callbacks
		activate: null,
		beforeStop: null,
		change: null,
		create: null,
		deactivate: null,
		out: null,
		over: null,
		receive: null,
		remove: null,
		sort: null,
		start: null,
		stop: null,
		update: null
	}
});
