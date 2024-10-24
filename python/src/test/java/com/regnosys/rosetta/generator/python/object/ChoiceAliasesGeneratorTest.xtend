package com.regnosys.rosetta.generator.python.object

import com.google.inject.Inject
import com.regnosys.rosetta.generator.python.PythonCodeGenerator
import com.regnosys.rosetta.tests.RosettaInjectorProvider
import com.regnosys.rosetta.tests.util.ModelHelper
import org.eclipse.xtext.testing.InjectWith
import org.eclipse.xtext.testing.extensions.InjectionExtension
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.^extension.ExtendWith

import static org.junit.jupiter.api.Assertions.*

@ExtendWith(InjectionExtension)
@InjectWith(RosettaInjectorProvider)
class ChoiceAliasGeneratorTest {

    @Inject extension ModelHelper
    @Inject PythonCodeGenerator generator;

    @Test
    def void testChoiceAliasGenerator() {
/*
            func Check1:
                inputs:
                    foo Foo (1..1)
                output:
                    result int (1..1)
                set result:
                    foo ->> deep1->attr 
*/
        val pythonCode = 
        '''
		type Bar1:
			deep1 Deep1 (1..1)
			b1 int (1..1)
			a int (1..1)

		type Bar2:
			deep1 Deep1 (1..1)
			b1 int (1..1)
			c int (1..1)

		type Bar3:
			bar2 Bar2(0..1)
			condition Choice: one-of 

		choice Foo:
			Bar1
			Bar3 

		type Deep1:
			attr int (1..1)
        '''.generatePython

/*		val classes = code.compileToClasses
        println ('***** function generator test dan 2 - Check1')
        val Check1 = classes.createFunc("Check1")
        println ('***** function generator test dan 2 - create fooBar1')
        val fooBar1 = classes.createInstanceUsingBuilder("Foo", #{
            "Bar1" -> classes.createInstanceUsingBuilder("Bar1", #{
                "Deep1" -> classes.createInstanceUsingBuilder("Deep1", #{
                    "attr" -> 42
                })
            })
        })
        println ('***** function generator test dan 2 - Check1 assert 42')
        assertEquals(42, Check1.invokeFunc(Integer, #[fooBar1]))
        println ('***** function generator test dan 2 - create fooBar3')
        val fooBar3 = classes.createInstanceUsingBuilder("Foo", #{
            "Bar3" -> classes.createInstanceUsingBuilder("Bar3", #{
                "Bar2" -> classes.createInstanceUsingBuilder("Bar2", #{
                    "Deep1" -> classes.createInstanceUsingBuilder("Deep1", #{
                        "attr" -> -1
                    })
                })
            })
        })
        println ('***** function generator test dan 2 - Check1 assert -1')
        assertEquals(-1, Check1.invokeFunc(Integer, #[fooBar3]))*/
        println ('***** testChoiceAliasGenerator - done')
    }
    def generatePython(CharSequence model) {
        val m = model.parseRosettaWithNoErrors
        val resourceSet = m.eResource.resourceSet
        val version = m.version
        
        val result = newHashMap
        result.putAll(generator.beforeAllGenerate(resourceSet, #{m}, version))
        result.putAll(generator.beforeGenerate(m.eResource, m, version))
        result.putAll(generator.generate(m.eResource, m, version))
        result.putAll(generator.afterGenerate(m.eResource, m, version))
        result.putAll(generator.afterAllGenerate(resourceSet, #{m}, version))
        
        result
    }
}