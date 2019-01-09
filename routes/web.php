<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
	$index = File::get(public_path() . '/dist/index.html');

	// $index = str_replace('href="styles','href="/dist/styles',$index);
	$index = str_replace('href="styles','href="/dist/styles',$index);

	$index = str_replace('src="','src="/dist/',$index);

    return $index;
});

Route::get('game/list', 'GameController@getList');
Route::get('game/getGameDataById', 'GameController@getGameDataById');

Route::get('game/test', 'GameController@test');


