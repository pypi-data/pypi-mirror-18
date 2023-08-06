
from phi import P, Obj, Rec, Make


class TestExamples(object):
    """docstring for TestExamples."""

    def test_example_1(self):

        text = "a bb ccc"
        avg_word_length = P.Pipe(
            text,
            Obj.split(" "), #['a', 'bb', 'ccc']
            P.map(len), #[1, 2, 3]
            list, # python 3 only
            P.sum() / len #6 / 3 == 2
        )

        assert 2 == avg_word_length


        text = "a bb ccc"
        avg_word_length = P.Pipe(
            text,
            Obj.split(" "), #['a', 'bb', 'ccc']
            P.map(len), #[1, 2, 3]
            list, # python 3 only
            Make(sum) / len #6 / 3 == 2
        )

        assert 2 == avg_word_length


        text = "a bb ccc"
        avg_word_length = P.Pipe(
            text,
            Obj.split(" "), #['a', 'bb', 'ccc']
            P.map(len), #[1, 2, 3]
            list, # python 3 only
            P.sum() / P.len() #6 / 3 == 2
        )

        assert 2 == avg_word_length


        avg_word_length = P.Pipe(
            "1 22 333",
            Obj.split(' '), # ['1', '22', '333']
            P.map(len), # [1, 2, 3]
            list, # python 3 only
            [
                sum # 1 + 2 + 3 == 6
            ,
                len # len([1, 2, 3]) == 3
            ],
            P[0] / P[1] # sum / len == 6 / 3 == 2
        )

        assert avg_word_length == 2

    def test_getting_started(self):
        from phi import P

        def add1(x): return x + 1
        def mul3(x): return x * 3

        x = P.Pipe(
            1.0,     #input 1
            add1,  #1 + 1 == 2
            mul3   #2 * 3 == 6
        )

        assert x == 6

        ################
        ################

        from phi import P

        x = P.Pipe(
            1.0,      #input 1
            P + 1,  #1 + 1 == 2
            P * 3   #2 * 3 == 6
        )

        assert x == 6

        ################
        ################

        from phi import P

        [x, y] = P.Pipe(
            1.0,  #input 1
            [
                P + 1  #1 + 1 == 2
            ,
                P * 3  #1 * 3 == 3
            ]
        )

        assert x == 2
        assert y == 3

        ################
        ################

        from phi import P

        [x, y] = P.Pipe(
            1.0,  #input 1
            P * 2,  #1 * 2 == 2
            [
                P + 1  #2 + 1 == 3
            ,
                P * 3  #2 * 3 == 6
            ]
        )

        assert x == 3
        assert y == 6

        ################
        ################

        from phi import P

        result = P.Pipe(
            1.0,  #input 1
            P * 2,  #1 * 2 == 2
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            )
        )

        assert result.x == 3
        assert result.y == 6

        ################
        ################

        from phi import P, Rec

        result = P.Pipe(
            1.0,  #input 1
            P * 2,  #1 * 2 == 2
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            Rec.x / Rec.y  #3 / 6 == 0.5
        )

        assert result == 0.5

        ################
        ################

        from phi import P, Rec

        [result, s] = P.Pipe(
            1.0,  #input 1
            P * 2, {'s'},  #2 * 1 == 2, saved as 's'
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            [
                Rec.x / Rec.y  #3 / 6 == 0.5
            ,
                's'  #load 's' == 2
            ]
        )

        assert result == 0.5
        assert s == 2

        ################
        ################

        from phi import P, Rec, Read

        [result, s] = P.Pipe(
            1.0,  #input 1
            P * 2, {'s'},  #2 * 1 == 2, saved as 's'
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            [
                Rec.x / Rec.y  #3 / 6 == 0.5
            ,
                Read.s + 3  # 2 + 3 == 5
            ]
        )

        assert result == 0.5
        assert s == 5

        ################
        ################

        from phi import P, Rec, Read, Write

        [result, s] = P.Pipe(
            1.0,  #input 1
            P * 2, Write.s,  #2 * 1 == 2, saved as 's'
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            [
                Rec.x / Rec.y  #3 / 6 == 0.5
            ,
                Read.s + 3  # 2 + 3 == 5
            ]
        )

        assert result == 0.5
        assert s == 5

        ################
        ################

        from phi import P, Rec, Val

        [result, s, val] = P.Pipe(
            1.0,  #input 1
            P * 2, Write.s,  #2 * 1 == 2, saved as 's'
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            [
                Rec.x / Rec.y  #3 / 6 == 0.5
            ,
                Read.s + 3  # 2 + 3 == 5
            ,
                Val(9) + 1  #input 9 and add 1, gives 10
            ]
        )

        assert result == 0.5
        assert s == 5
        assert val == 10

        #########################
        #########################

        from phi import P, Rec, Read, Write, Val, If

        [result, s, val] = P.Pipe(
            1.0,  #input 1
            (P + 3) / (P + 1), Write.s,  #4 / 2 == 2, saved as 's'
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            [
                Rec.x / Rec.y  #3 / 6 == 0.5
            ,
                Read.s + 3  # 2 + 3 == 5
            ,
                If( Rec.y > 7,
                    Val(9) + 1  #input 9 and add 1, gives 10
                ).Else(
                    Val("Sorry, come back latter.")
                )
            ]
        )

        assert result == 0.5
        assert s == 5
        assert val == "Sorry, come back latter."


        ######################################
        #######################################

        from phi import P, Rec, Read, Write, Val, If

        f = P.Make(
            (P + 3) / (P + 1), Write.s,  #4 / 2 == 2, saved as 's'
            dict(
                x = P + 1  #2 + 1 == 3
            ,
                y = P * 3  #2 * 3 == 6
            ),
            [
                Rec.x / Rec.y  #3 / 6 == 0.5
            ,
                Read.s + 3  # 2 + 3 == 5
            ,
                If( Rec.y > 7,
                    Val(9) + 1  #input 9 and add 1, gives 10
                ).Else(
                    Val("Sorry, come back latter.")
                )
            ]
        )

        [result, s, val] = f(1.0)

        assert result == 0.5
        assert s == 5
        assert val == "Sorry, come back latter."



    def test_builder_NMake(self):

        from phi import P

        assert 1 == P.Pipe(
            1, {'s'}, # write s == 1, outer context
            P.Make(
                P + 1, {'s'} # write s == 2, inner context
            ),
            's'  # read s == 1, outer context
        )

        #############################
        #############################

        from phi import P

        assert 2 == P.Pipe(
            1, {'s'},   #write s == 1, same context
            P.Make(
                P + 1, {'s'},   #write s == 2, same context
                create_ref_context=False
            ),
            's'   # read s == 2, same context
        )


        #############################
        #############################

        from phi import P

        assert 2 == P.Pipe(
            1, {'s'},   #write s == 1, same context
            P.NMake(
                P + 1, {'s'}   #write s == 2, same context
            ),
            's'   # read s == 2, same context
        )


        ################################
        ################################




    def test_builder_NPipe(self):

        from phi import P

        assert 1 == P.Pipe(
            1, {'s'}, # write s == 1, outer context
            lambda x: P.Pipe(
                x,
                P + 1, {'s'} # write s == 2, inner context
            ),
            's'  # read s == 1, outer context
        )

        #############################
        #############################

        from phi import P

        assert 2 == P.Pipe(
            1, {'s'},   #write s == 1, same context
            lambda x: P.Pipe(
                x,
                P + 1, {'s'},   #write s == 2, same context
                create_ref_context=False
            ),
            's'   # read s == 2, same context
        )

        #############################
        #############################

        from phi import P

        assert 2 == P.Pipe(
            1, {'s'},   #write s == 1, same context
            lambda x: P.NPipe(
                x,
                P + 1, {'s'}   #write s == 2, same context
            ),
            's'   # read s == 2, same context
        )

        #############################
        #############################

    def test_not(self):

        from phi import P

        assert True == P.Pipe(
            1,
            P + 1,  # 1 + 1 == 2
            P > 5,  # 2 > 5 == False
            P.Not() # not False == True
        )

        ################################
        ################################

        from phi import P

        assert True == P.Pipe(
            1,
            (P + 1 > 5).Not()  # not 1 + 1 > 5 == not 2 > 5 == not False == True
        )

        ############################
        #############################

        from phi import P

        f = (P + 1 > 5).Not()   #lambda x: not x + 1 > 5

        assert f(1) == True

    def test_contains(self):

        from phi import P

        assert False == P.Pipe(
            [1,2,3,4],
            P.filter(P % 2 != 0)   #[1, 3], keeps odds
            .Contains(4)   #4 in [1, 3] == False
        )

    def test_ref(self):

        from phi import P, Obj, Ref

        assert {'a': 97, 'b': 98, 'c': 99} == P.Pipe(
            "a b c", Obj
            .split(' ').Write['keys']  # keys = ['a', 'b', 'c']
            .map(ord),  # [ord('a'), ord('b'), ord('c')] == [97, 98, 99]
            lambda it: zip(Ref.keys, it),  # [('a', 97), ('b', 98), ('c', 99)]
            dict   # {'a': 97, 'b': 98, 'c': 99}
        )

    def test_if(self):

        from phi import P, Val

        assert "Less or equal to 10" == P.Pipe(
            5,
            P.If(P > 10,
                Val("Greater than 10"),
            Else = (
                Val("Less or equal to 10")
            ))
        )

        #########################
        #########################

        from phi import P, Val, If

        assert "Less or equal to 10" == P.Pipe(
            5,
            If(P > 10,
                Val("Greater than 10")
            )
            .Else(
                Val("Less or equal to 10")
            )
        )